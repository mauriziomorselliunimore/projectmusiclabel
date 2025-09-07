from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from reviews.models import Review
from api.serializers import ReviewSerializer
from reviews.cache import get_user_ratings

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Restituisce le recensioni filtrate in base ai parametri della richiesta.
        """
        queryset = Review.objects.select_related('reviewer', 'reviewed').all()
        
        # Filtra per tipo di recensione
        review_type = self.request.query_params.get('type', None)
        if review_type:
            queryset = queryset.filter(review_type=review_type)
        
        # Filtra per utente recensito
        reviewed_id = self.request.query_params.get('reviewed', None)
        if reviewed_id:
            queryset = queryset.filter(reviewed_id=reviewed_id)
        
        return queryset

    def perform_create(self, serializer):
        """
        Salva il recensore come utente corrente.
        """
        serializer.save(reviewer=self.request.user)

    @method_decorator(cache_page(60 * 15))  # Cache per 15 minuti
    @action(detail=False, methods=['get'])
    def ratings_summary(self, request):
        """
        Restituisce un riepilogo delle valutazioni per un utente specifico.
        """
        user_id = request.query_params.get('user_id')
        review_type = request.query_params.get('type')
        
        if not user_id or not review_type:
            return Response({
                'error': 'Parametri user_id e type sono richiesti'
            }, status=400)
            
        ratings = get_user_ratings(user_id, review_type)
        return Response(ratings)
        
    def get_permissions(self):
        """
        Personalizza i permessi in base all'azione.
        """
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()
