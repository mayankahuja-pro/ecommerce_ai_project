from .models import Product, UserInteraction
import numpy as np

# Try to import the Cython-optimized function
try:
    from .price_similarity import compute_similarity as cython_compute_similarity
    HAS_CYTHON = True
except (ImportError, ModuleNotFoundError):
    HAS_CYTHON = False

def python_compute_similarity(prices, avg_price):
    """Fallback Python/NumPy implementation of price similarity."""
    return np.abs(prices - avg_price)

def recommend_products(request, top_n=4):
    user = request.user
    session_key = request.session.session_key
    
    # 1. Get user interactions (Support both logged-in and guest users)
    if user.is_authenticated:
        interactions = UserInteraction.objects.filter(user=user, liked=True)
    elif session_key:
        interactions = UserInteraction.objects.filter(session_key=session_key, liked=True)
    else:
        interactions = UserInteraction.objects.none()

    # 2. Cold Start: If no likes yet, show random products
    if not interactions.exists():
        return Product.objects.all().order_by('?')[:top_n]

    # 3. Calculate Average Price of liked items
    liked_products = [i.product for i in interactions]
    liked_prices = np.array([p.price for p in liked_products])
    avg_price = liked_prices.mean()

    # 4. Filter out items already liked
    candidates = Product.objects.exclude(
        id__in=[p.id for p in liked_products]
    )
    
    candidate_list = list(candidates)
    if not candidate_list:
        return []

    # 5. Compute Similarity scores
    prices = np.array([p.price for p in candidate_list], dtype=np.float64)
    
    if HAS_CYTHON:
        try:
            similarity_scores = cython_compute_similarity(prices, avg_price)
        except Exception:
            # Final fallback if Cython fails at runtime
            similarity_scores = python_compute_similarity(prices, avg_price)
    else:
        similarity_scores = python_compute_similarity(prices, avg_price)

    # 6. Sort and return top N
    product_scores = list(zip(candidate_list, similarity_scores))
    product_scores.sort(key=lambda x: x[1])

    return [p[0] for p in product_scores[:top_n]]
