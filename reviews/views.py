from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.db.models import Avg, Q

from .models import Review
from .forms import ReviewForm

@login_required
def create_review(request, user_id):
    reviewed_user = get_object_or_404(User, id=user_id)
    
    # Determina il tipo di recensione in base ai ruoli
    if hasattr(request.user, 'artist') and hasattr(reviewed_user, 'associate'):
        review_type = 'artist_to_associate'
    elif hasattr(request.user, 'associate') and hasattr(reviewed_user, 'artist'):
        review_type = 'associate_to_artist'
    else:
        messages.error(request, 'Non hai i permessi per lasciare questa recensione')
        return redirect('home')
    
    # Verifica se esiste già una recensione
    existing_review = Review.objects.filter(reviewer=request.user, reviewed=reviewed_user).first()
    if existing_review:
        messages.warning(request, 'Hai già lasciato una recensione per questo utente')
        return redirect('reviews:detail', review_id=existing_review.id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, review_type=review_type)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.reviewed = reviewed_user
            review.review_type = review_type
            review.save()
            
            messages.success(request, 'Recensione pubblicata con successo!')
            if review_type == 'artist_to_associate':
                return redirect('associates:detail', pk=reviewed_user.associate.id)
            else:
                return redirect('artists:detail', pk=reviewed_user.artist.id)
    else:
        form = ReviewForm(review_type=review_type)
    
    context = {
        'form': form,
        'reviewed_user': reviewed_user,
        'review_type': review_type
    }
    return render(request, 'reviews/create_review.html', context)

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    
    # Verifica che l'utente sia il proprietario della recensione
    if review.reviewer != request.user:
        raise PermissionDenied
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review, review_type=review.review_type)
        if form.is_valid():
            form.save()
            messages.success(request, 'Recensione aggiornata con successo!')
            return redirect('reviews:detail', review_id=review.id)
    else:
        form = ReviewForm(instance=review, review_type=review.review_type)
    
    context = {
        'form': form,
        'review': review,
        'reviewed_user': review.reviewed
    }
    return render(request, 'reviews/edit_review.html', context)

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    
    # Verifica che l'utente sia il proprietario della recensione
    if review.reviewer != request.user:
        raise PermissionDenied
    
    if request.method == 'POST':
        reviewed_user = review.reviewed
        review.delete()
        messages.success(request, 'Recensione eliminata con successo!')
        
        # Redirect in base al tipo di recensione
        if review.review_type == 'artist_to_associate':
            return redirect('associates:detail', pk=reviewed_user.associate.id)
        else:
            return redirect('artists:detail', pk=reviewed_user.artist.id)
    
    context = {'review': review}
    return render(request, 'reviews/delete_review.html', context)

def user_reviews(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    # Verifica i permessi di visualizzazione
    if not request.user.is_authenticated:
        raise PermissionDenied
    
    # Per gli artisti, mostra solo le recensioni degli associati
    if hasattr(user, 'artist'):
        if not hasattr(request.user, 'associate'):
            raise PermissionDenied
        reviews = Review.objects.filter(
            reviewed=user,
            review_type='associate_to_artist'
        )
    # Per gli associati, mostra solo le recensioni degli artisti
    elif hasattr(user, 'associate'):
        if not hasattr(request.user, 'artist'):
            raise PermissionDenied
        reviews = Review.objects.filter(
            reviewed=user,
            review_type='artist_to_associate'
        )
    else:
        raise PermissionDenied
    
    # Calcola le medie delle valutazioni
    avg_ratings = reviews.aggregate(
        avg_rating=Avg('rating'),
        avg_professionalism=Avg('professionalism'),
        avg_communication=Avg('communication'),
        avg_value=Avg('value'),
        avg_reliability=Avg('reliability'),
        avg_preparation=Avg('preparation'),
        avg_collaboration=Avg('collaboration')
    )
    
    context = {
        'reviewed_user': user,
        'reviews': reviews,
        'avg_ratings': avg_ratings,
        'total_reviews': reviews.count()
    }
    return render(request, 'reviews/user_reviews.html', context)
