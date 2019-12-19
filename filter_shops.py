def filter_shops(shops, only_opening, min_rate, max_rate):
    return list(
        filter(
            lambda shop: (only_opening == False or shop["opening_now"])
            and (min_rate <= shop["rating"] and shop["rating"] <= max_rate),
            shops,
        )
    )
