def compute_momentum(returns):
    return round(sum(returns)/len(returns), 2) if returns else 0