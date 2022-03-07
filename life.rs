use std::{collections::{ HashSet, HashMap }, ops::Add};

#[derive(PartialEq, Eq, Hash)]
struct Cell {
    x: i64,
    y: i64,
}

const LIVE_RULES: [i8; 2] = [2, 3];
const SPAWN_RULES: [i8; 1] = [3];
const OFFSETS: [Cell; 8] = [
    Cell{x:-1, y:1}, Cell{x:0, y:1}, Cell{x:1, y:1},
    Cell{x:-1, y:0},                 Cell{x:1, y:0},
    Cell{x:-1,y:-1}, Cell{x:0,y:-1}, Cell{x:1,y:-1}
];


pub struct GameOfLife {
    living_cells: HashSet<Cell>
}

impl GameOfLife {
    fn living_neighbors(cell: Cell) -> Vec<Cell> {
        let mut neighbors = Vec::new();
        for offset in OFFSETS {
            let neighbor = Cell{
                x: cell.x + offset.x,
                y: cell.y + offset.y,
            };
            neighbors.push(neighbor);

        }
        neighbors
    }

    pub fn evolve(&mut self) {
        let mut hopefuls: HashMap<Cell, i8> = HashMap::new();
        let mut next_state: HashSet<Cell> = HashSet::new();

        for cell in &self.living_cells {
            let mut neighbors_alive: i8 = 0;

            for offset in OFFSETS {
                let poss = Cell{x: cell.x + offset.x, y: cell.y + offset.y};
                if self.living_cells.contains(&poss) {
                    neighbors_alive += 1;
                } else {
                    *hopefuls.entry(poss).or_insert(0) += 1;
                }
            }
            if LIVE_RULES.contains(&neighbors_alive) {
                next_state.insert(Cell{x:cell.x, y:cell.y});
            }
        }
        for cell in hopefuls.keys() {
            if SPAWN_RULES.contains(hopefuls.get(cell).unwrap()) {
                next_state.insert(Cell{x:cell.x, y:cell.y});
            }
        }
        self.living_cells = next_state;
    }
}