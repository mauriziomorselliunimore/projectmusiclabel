from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Associate, PortfolioItem
from .forms import AssociateForm, PortfolioItemForm

def associate_list(request):
    """Lista tutti gli associati con ricerca"""
    query = request.GET.get('search', '')
    skill_filter = request.GET.get('skill', '')
    location_filter = request.GET.get('location', '')
    
    associates = Associate.objects.filter(is_active=True, is_available=True)
    
    if query:
        associates = associates.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(specialization__icontains=query) |
            Q(skills__icontains=query) |
            Q(bio__icontains=query)
        )
    
    if skill_filter:
        associates = associates.filter(skills__icontains=skill_filter)
    
    if location_filter:
        associates = associates.filter(location__icontains=location_filter)
    
    context = {
        'associates': associates,
        'search_query': query,
        'skill_filter': skill_filter,
        'location_filter': location_filter,
    }
    return render(request, 'associates/associate_list.html', context)

def associate_detail(request, pk):
    """Dettaglio singolo associato"""
    associate = get_object_or_404(Associate, pk=pk, is_active=True)
    portfolio_items = associate.portfolio_items.all()
    
    context = {
        'associate': associate,
        'portfolio_items': portfolio_items,
        'is_owner': request.user == associate.user,
    }
    return render(request, 'associates/associate_detail.html', context)

@login_required
def associate_create(request):
    """Crea profilo associato"""
    # Check if user already has an associate profile
    if hasattr(request.user, 'associate'):
        messages.info(request, 'Hai già un profilo associato!')
        return redirect('associates:detail', pk=request.user.associate.pk)
    
    if request.method == 'POST':
        form = AssociateForm(request.POST)
        if form.is_valid():
            associate = form.save(commit=False)
            associate.user = request.user
            associate.save()
            messages.success(request, 'Profilo associato creato con successo!')
            return redirect('associates:detail', pk=associate.pk)
    else:
        form = AssociateForm()
    
    return render(request, 'associates/associate_form.html', {'form': form, 'title': 'Crea Profilo Associato'})

@login_required
def associate_edit(request, pk):
    """Modifica profilo associato"""
    associate = get_object_or_404(Associate, pk=pk)
    
    # Check ownership
    if associate.user != request.user:
        messages.error(request, 'Non hai i permessi per modificare questo profilo!')
        return redirect('associates:detail', pk=pk)
    
    if request.method == 'POST':
        form = AssociateForm(request.POST, instance=associate)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profilo aggiornato con successo!')
            return redirect('associates:detail', pk=pk)
    else:
        form = AssociateForm(instance=associate)
    
    return render(request, 'associates/associate_form.html', {'form': form, 'title': 'Modifica Profilo'})

@login_required
def portfolio_add(request):
    """Aggiungi elemento al portfolio"""
    if not hasattr(request.user, 'associate'):
        messages.error(request, 'Devi avere un profilo associato per aggiungere elementi al portfolio!')
        return redirect('associates:create')
    
    if request.method == 'POST':
        form = PortfolioItemForm(request.POST, request.FILES)
        if form.is_valid():
            portfolio_item = form.save(commit=False)
            portfolio_item.associate = request.user.associate
            portfolio_item.save()
            messages.success(request, f'Elemento "{portfolio_item.title}" aggiunto al portfolio!')
            return redirect('associates:detail', pk=request.user.associate.pk)
    else:
        form = PortfolioItemForm()
    
    return render(request, 'associates/portfolio_form.html', {'form': form})

@login_required
def portfolio_delete(request, pk):
    """Elimina elemento portfolio"""
    portfolio_item = get_object_or_404(PortfolioItem, pk=pk)
    
    # Check ownership
    if portfolio_item.associate.user != request.user:
        messages.error(request, 'Non hai i permessi per eliminare questo elemento!')
        return redirect('associates:detail', pk=portfolio_item.associate.pk)
    
    if request.method == 'POST':
        portfolio_item.delete()
        messages.success(request, 'Elemento eliminato dal portfolio!')
        return redirect('associates:detail', pk=portfolio_item.associate.pk)
    
    return render(request, 'associates/portfolio_confirm_delete.html', {'portfolio_item': portfolio_item})