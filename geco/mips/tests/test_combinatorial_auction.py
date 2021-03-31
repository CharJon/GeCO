import itertools

import pytest

from geco.mips.combinatorial_auction.gasse import gasse_params, gasse_instance
from geco.mips.combinatorial_auction.generic import combinatorial_auction


def test_simple_instance():
    bids = [([0], 2)]
    n_dummy_items = 0
    n_items = 1
    instance = combinatorial_auction(
        bids=bids, n_dummy_items=n_dummy_items, n_items=n_items
    )
    instance.hideOutput()
    instance.optimize()
    assert instance.getObjectiveSense() == "maximize"
    assert instance.getNVars() == len(bids)
    assert instance.getNConss() == n_items
    assert instance.getStatus() == "optimal"
    assert instance.getObjVal() == 2  # optimal value is the price of the only bid


def test_gasse_instance_creation():
    n_bids = 1
    n_items = 1
    model = gasse_instance(
        n_items=n_items,
        n_bids=n_bids,
        min_value=1,
        max_value=2,
        value_deviation=0,
        add_item_prob=1,
        max_n_sub_bids=1,
        seed=0,
    )
    assert model.getObjectiveSense() == "maximize"
    assert model.getNVars() == n_bids
    assert model.getNConss() == n_items


@pytest.mark.parametrize(
    "n_items, n_bids, min_value, max_value, value_deviation, add_item_prob, max_n_sub_bids, additivity, "
    "budget_factor, resale_factor, integers, warnings, seed1, seed2",
    itertools.product(
        [5, 10, 100],
        [500],
        [1],
        [100],
        [-0.5, 0.5],
        [0.9],
        [5],
        [0.2],
        [1.5],
        [0.5, 1],
        [True, False],
        [True, False],
        [1, 1337],
        [1, 1337],
    ),
)
def test_gasse_seeding(
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
    seed1,
    seed2,
):
    params1 = gasse_params(
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
        seed=seed1,
    )
    params2 = gasse_params(
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
        seed=seed2,
    )
    same_seeds_produce_same_params = seed1 == seed2 and params1 == params2
    different_seeds_produce_different_params = seed1 != seed2 and params1 != params2
    assert same_seeds_produce_same_params or different_seeds_produce_different_params
