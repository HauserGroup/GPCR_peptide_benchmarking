from scipy import stats


def get_spearman_correlation(x, y):
    rho, p_value = stats.spearmanr(x, y)
    return rho, p_value
