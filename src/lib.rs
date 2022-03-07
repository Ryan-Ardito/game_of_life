use pyo3::prelude::*;
use std::{collections::{ HashSet, HashMap }};

const LIVE_RULES: [i8; 2] = [2, 3];
const SPAWN_RULES: [i8; 1] = [3];
const OFFSETS: [(i64, i64); 8] = [
    (-1, 1), (0, 1), (1, 1),
    (-1, 0),         (1, 0),
    (-1,-1), (0,-1), (1,-1)
];


fn living_neighbors(cell: (i64, i64)) -> Vec<(i64, i64)> {
    let mut neighbors = Vec::new();
    for offset in OFFSETS {
        let neighbor = (
            cell.0 + offset.0,
            cell.1 + offset.1,
        );
        neighbors.push(neighbor);

    }
    neighbors
}

#[pyfunction]
pub fn evolve(living_cells: HashSet<(i64, i64)>) -> HashSet<(i64, i64)> {
    let mut hopefuls: HashMap<(i64, i64), i8> = HashMap::new();
    let mut next_state: HashSet<(i64, i64)> = HashSet::new();

    for cell in &living_cells {
        let mut neighbors_alive: i8 = 0;

        for offset in OFFSETS {
            let poss = (cell.0 + offset.0, cell.1 + offset.1);
            if living_cells.contains(&poss) {
                neighbors_alive += 1;
            } else {
                *hopefuls.entry(poss).or_insert(0) += 1;
            }
        }
        if LIVE_RULES.contains(&neighbors_alive) {
            next_state.insert((cell.0, cell.1));
        }
    }
    for cell in hopefuls.keys() {
        if SPAWN_RULES.contains(hopefuls.get(cell).unwrap()) {
            next_state.insert((cell.0, cell.1));
        }
    }
    next_state
}

/// A Python module implemented in Rust.
#[pymodule]
fn game_of_life(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(evolve, m)?)?;
    Ok(())
}