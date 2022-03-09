use pyo3::prelude::*;
use std::{collections::{ HashSet, HashMap }};


const LIVE_RULES: [i8; 2] = [2, 3];
const SPAWN_RULES: [i8; 1] = [3];
const OFFSETS: [(i64, i64); 8] = [
    (-1, 1), (0, 1), (1, 1),
    (-1, 0),         (1, 0),
    (-1,-1), (0,-1), (1,-1)
];


#[pyclass]
pub struct GameOfLife {
    living_cells: HashSet<(i64, i64)>
}

#[pymethods]
impl GameOfLife {

    #[new]
    fn new(pattern: HashSet<(i64, i64)>) -> Self {
        GameOfLife {
            living_cells: pattern
        }
    }

    pub fn evolve(&mut self) {
        let mut hopefuls: HashMap<(i64, i64), i8> = HashMap::new();
        let mut next_state: HashSet<(i64, i64)> = HashSet::new();

        for cell in &self.living_cells {
            let mut neighbors_alive: i8 = 0;

            for offset in OFFSETS {
                let poss = (cell.0 + offset.0, cell.1 + offset.1);
                if self.living_cells.contains(&poss) {
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
        self.living_cells = next_state;
    }

    pub fn bounded_set(&self, width: i64, height: i64) -> HashSet<(i64, i64)> {
        // Generate a set of live cells within a window and adjust coordinates
        let mut grid_window = HashSet::new();
        let a = width / 2;
        let b = height / 2;
        for cell in &self.living_cells {
            let x = cell.0;
            let y = cell.1;
            let cell = (x+a, b+y);
            if (cell.1 < 0) || (cell.1 > height) {
                continue
            } else if (cell.0 < 0) || (cell.0 > width) {
                continue
            }
            grid_window.insert((cell.0, cell.1));
        }
        grid_window
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn game_of_life(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<GameOfLife>()?;
    Ok(())
}