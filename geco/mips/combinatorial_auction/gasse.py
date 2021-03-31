import numpy as np
from networkx.utils import np_random_state

from geco.mips.combinatorial_auction.generic import combinatorial_auction


@np_random_state(-1)
def gasse_instance(
    n_items=100,
    n_bids=500,
    min_value=1,
    max_value=100,
    value_deviation=0.5,
    add_item_prob=0.9,
    max_n_sub_bids=5,
    additivity=0.2,
    budget_factor=1.5,
    resale_factor=0.5,
    integers=False,
    warnings=False,
    seed=0,
):
    """
    Generate a Combinatorial Auction instance following the 'arbitrary' scheme found in section 4.3. of [1].

    Parameters
    ----------
    n_items: int
        The number of items
    n_bids: int
        The number of bids
    min_value: int
        The minimum resale value for an item
    max_value: int
        The maximum resale value for an item
    value_deviation: float
        The deviation allowed for each bidder's private value of an item, relative from max_value
    add_item_prob: float between 0 and 1
        The probability of adding a new item to an existing bundle
    max_n_sub_bids: int
        The maximum number of substitutable bids per bidder (+1 gives the maximum number of bids per bidder)
    additivity: float
        Additivity parameter for bundle prices. Note that additivity < 0 gives sub-additive bids, while additivity > 0 gives super-additive bids
    budget_factor: float
        The budget factor for each bidder, relative to their initial bid's price
    resale_factor: float
        The resale factor for each bidder, relative to their initial bid's resale value
    integers: logical
        Should bid's prices be integral ?
    warnings: logical
        Should warnings be printed ?
    seed: integer, random_state, or None
        Indicator of random number generation state

    Returns
    -------
    model: scip.Model
        A pyscipopt model of the generated instance

    References
    ----------
    .. [1] Kevin Leyton-Brown, Mark Pearson, and Yoav Shoham. (2000).
    Towards a universal test suite for combinatorial auction algorithms.
    Proceedings of ACM Conference on Electronic Commerce (EC-00) 66-76.
    """
    return combinatorial_auction(
        *gasse_params(
            n_items,
            n_bids,
            min_value,
            max_value,
            value_deviation,
            add_item_prob,
            max_n_sub_bids,
            additivity,
            budget_factor,
            resale_factor,
            integers,
            warnings,
            seed,
        ),
        n_items=n_items,
        name="Gasse Combinatorial Auction"
    )


@np_random_state(-1)
def gasse_params(
    n_items=100,
    n_bids=500,
    min_value=1,
    max_value=100,
    value_deviation=0.5,
    add_item_prob=0.9,
    max_n_sub_bids=5,
    additivity=0.2,
    budget_factor=1.5,
    resale_factor=0.5,
    integers=False,
    warnings=False,
    seed=0,
):
    """
    Generate a Combinatorial Auction instance params following the 'arbitrary' scheme found in section 4.3. of [1].
    This is based on the code from [2].

    Parameters
    ----------
    n_items: int
        The number of items
    n_bids: int
        The number of bids
    min_value: int
        The minimum resale value for an item
    max_value: int
        The maximum resale value for an item
    value_deviation: float
        The deviation allowed for each bidder's private value of an item, relative from max_value
    add_item_prob: float between 0 and 1
        The probability of adding a new item to an existing bundle
    max_n_sub_bids: int
        The maximum number of substitutable bids per bidder (+1 gives the maximum number of bids per bidder)
    additivity: float
        Additivity parameter for bundle prices. Note that additivity < 0 gives sub-additive bids, while additivity > 0 gives super-additive bids
    budget_factor: float
        The budget factor for each bidder, relative to their initial bid's price
    resale_factor: float
        The resale factor for each bidder, relative to their initial bid's resale value
    integers: logical
        Should bid's prices be integral ?
    warnings: logical
        Should warnings be printed ?
    seed: integer, random_state, or None
        Indicator of random number generation state

    Returns
    -------
    bids: list[tuple[list, float]]
        A list of bids each represented by a tuple of a bundle and the price proposed
    n_dummy_items: int
        Number of dummy items added to each bid

    References
    ----------
    .. [1] Kevin Leyton-Brown, Mark Pearson, and Yoav Shoham. (2000).
    Towards a universal test suite for combinatorial auction algorithms.
    Proceedings of ACM Conference on Electronic Commerce (EC-00) 66-76.
    .. [2] https://github.com/ds4dm/learn2branch/blob/master/01_generate_instances.py
    """
    assert min_value >= 0 and max_value >= min_value
    assert add_item_prob >= 0 and add_item_prob <= 1

    def choose_next_item(bundle_mask, interests, compats, add_item_prob, seed):
        n_items = len(interests)
        prob = (1 - bundle_mask) * interests * compats[bundle_mask, :].mean(axis=0)
        prob /= prob.sum()
        return seed.choice(n_items, p=prob)

    # common item values (resale price)
    values = min_value + (max_value - min_value) * seed.rand(n_items)

    # item compatibilities
    compats = np.triu(seed.rand(n_items, n_items), k=1)
    compats = compats + compats.transpose()
    compats = compats / compats.sum(1)

    bids = []
    n_dummy_items = 0

    # create bids, one bidder at a time
    while len(bids) < n_bids:

        # bidder item values (buy price) and interests
        private_interests = seed.rand(n_items)
        private_values = values + max_value * value_deviation * (
            2 * private_interests - 1
        )

        # substitutable bids of this bidder
        bidder_bids = {}

        # generate initial bundle, choose first item according to bidder interests
        prob = private_interests / private_interests.sum()
        item = seed.choice(n_items, p=prob)
        bundle_mask = np.full(n_items, 0)
        bundle_mask[item] = 1

        # add additional items, according to bidder interests and item compatibilities
        while seed.rand() < add_item_prob:
            # stop when bundle full (no item left)
            if bundle_mask.sum() == n_items:
                break
            item = choose_next_item(
                bundle_mask, private_interests, compats, add_item_prob, seed
            )
            bundle_mask[item] = 1

        bundle = np.nonzero(bundle_mask)[0]

        # compute bundle price with value additivity
        price = private_values[bundle].sum() + np.power(len(bundle), 1 + additivity)
        if integers:
            price = int(price)

        # drop negativaly priced bundles
        if price < 0:
            if warnings:
                print("warning: negatively priced bundle avoided")
            continue

        # bid on initial bundle
        bidder_bids[frozenset(bundle)] = price

        # generate candidates substitutable bundles
        sub_candidates = []
        for item in bundle:

            # at least one item must be shared with initial bundle
            bundle_mask = np.full(n_items, 0)
            bundle_mask[item] = 1

            # add additional items, according to bidder interests and item compatibilities
            while bundle_mask.sum() < len(bundle):
                item = choose_next_item(
                    bundle_mask, private_interests, compats, add_item_prob, seed
                )
                bundle_mask[item] = 1

            sub_bundle = np.nonzero(bundle_mask)[0]

            # compute bundle price with value additivity
            sub_price = private_values[sub_bundle].sum() + np.power(
                len(sub_bundle), 1 + additivity
            )
            if integers:
                sub_price = int(sub_price)

            sub_candidates.append((sub_bundle, sub_price))

        # filter valid candidates, higher priced candidates first
        budget = budget_factor * price
        min_resale_value = resale_factor * values[bundle].sum()
        for bundle, price in [
            sub_candidates[i]
            for i in np.argsort([-price for bundle, price in sub_candidates])
        ]:

            if (
                len(bidder_bids) >= max_n_sub_bids + 1
                or len(bids) + len(bidder_bids) >= n_bids
            ):
                break

            if price < 0:
                if warnings:
                    print("warning: negatively priced substitutable bundle avoided")
                continue

            if price > budget:
                if warnings:
                    print("warning: over priced substitutable bundle avoided")
                continue

            if values[bundle].sum() < min_resale_value:
                if warnings:
                    print(
                        "warning: substitutable bundle below min resale value avoided"
                    )
                continue

            if frozenset(bundle) in bidder_bids:
                if warnings:
                    print("warning: duplicated substitutable bundle avoided")
                continue

            bidder_bids[frozenset(bundle)] = price

        # add XOR constraint if needed (dummy item)
        if len(bidder_bids) > 2:
            dummy_item = [n_items + n_dummy_items]
            n_dummy_items += 1
        else:
            dummy_item = []

        # place bids
        for bundle, price in bidder_bids.items():
            bids.append((list(bundle) + dummy_item, price))

        return bids, n_dummy_items
