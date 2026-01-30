# from .models import Product, UserInteraction
# import numpy as np

# def recommend_products(user, top_n=4):
#     interactions = UserInteraction.objects.filter(user=user, liked=True)

#     if not interactions.exists():
#         # Cold start → show popular or random
#         return Product.objects.all()[:top_n]

#     liked_products = [i.product for i in interactions]
#     liked_prices = np.array([p.price for p in liked_products])

#     avg_price = liked_prices.mean()

#     # Recommend products with similar price range
#     recommendations = Product.objects.exclude(
#         id__in=[p.id for p in liked_products]
#     ).order_by('price')

#     similar_products = sorted(
#         recommendations,
#         key=lambda p: abs(p.price - avg_price)
#     )

#     return similar_products[:top_n]





from .models import Product, UserInteraction
import numpy as np
from .price_similarity import compute_similarity

def recommend_products(user, top_n=4):
    interactions = UserInteraction.objects.filter(user=user, liked=True)

    if not interactions.exists():
        return Product.objects.all()[:top_n]

    liked_products = [i.product for i in interactions]
    avg_price = np.mean([p.price for p in liked_products])

    candidates = Product.objects.exclude(
        id__in=[p.id for p in liked_products]
    )

    prices = np.array([p.price for p in candidates], dtype=np.float64)

    # ⚡ CYTHON OPTIMIZED PART
    similarity_scores = compute_similarity(prices, avg_price)

    product_scores = list(zip(candidates, similarity_scores))
    product_scores.sort(key=lambda x: x[1])

    return [p[0] for p in product_scores[:top_n]]

