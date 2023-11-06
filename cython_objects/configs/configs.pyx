cdef class ScreenConfig:
    def __cinit__(self,
                  background_color: tuple = (180, 180, 180),
                  border_color: tuple = (170, 170, 170),
                  window_width: int = 1800,
                  window_height: int = 900,
                  ):
        self.background_color = background_color
        self.border_color = border_color
        self.window_width = window_width
        self.window_height = window_height

cdef class CellActionsCostConfig:
    def __init__(self,
                 int check_energy = 1,
                 int check_cell_in_front = 1,
                 turn: int = 1,
                 get_minerals_energy: int = 5,
                 photosynthesis: int = 5,
                 move: int = 26,
                 eat: int = 2
                 ):
        self.actions_costs = {
            21: check_energy,
            22: check_cell_in_front,
            23: turn,
            24: get_minerals_energy,
            25: photosynthesis,
            26: move,
            27: eat
        }

cdef class CellConfig:
    def __init__(self,
                 cell_size: int = 35,
                 cell_mutation_chance: int = 100,
                 cell_energy_to_live: int = 3,
                 eat_gain_energy: int = 20,
                 cells_available_actions_count: int = 5,
                 CellActionsCostConfig actions_costs = CellActionsCostConfig(),
                 start_cell_energy: int = 50,
                 max_cell_energy: int = 150,
                 genome_size: int = 64,
                 int max_x_id = 51,
                 int max_y_id = 25,
                 ):
        self.cell_size = cell_size
        self.cell_mutation_chance = cell_mutation_chance
        self.cell_energy_to_live = cell_energy_to_live
        self.eat_gain_energy = eat_gain_energy
        self.cells_available_actions_count = cells_available_actions_count
        self.actions_costs = actions_costs.actions_costs
        self.start_cell_energy = start_cell_energy
        self.max_cell_energy = max_cell_energy
        self.genome_size = genome_size
        self.max_x_id = max_x_id
        self.max_y_id = max_y_id

cdef class GameConfig:
    def __init__(self,
                 seed: int,
                 CellConfig cell_config,
                 ScreenConfig screen_config,
                 flip_interval: int = 120
                 ):
        self.seed = seed
        self.cell_config = cell_config
        self.screen_config = screen_config
        self.flip_interval = flip_interval
        self.stop = False
