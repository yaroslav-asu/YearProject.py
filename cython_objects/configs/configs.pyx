cdef class ScreenConfig:
    def __init__(self,
                 tuple background_color = (180, 180, 180),
                 int window_width = 1800,
                 int window_height = 900,
                 ):
        self.background_color = background_color
        self.window_width = window_width
        self.window_height = window_height

cdef class CellActionsCostConfig:
    def __init__(self,
                 int check_energy = 1,
                 int check_cell_in_front = 1,
                 turn: int = 1,
                 get_minerals_energy: int = 5,
                 photosynthesis: int = 5,
                 move: int = 1,
                 eat: int = 2
                 ):
        self.actions_costs = {
            1: check_energy,
            2: check_cell_in_front,
            3: turn,
            4: get_minerals_energy,
            5: photosynthesis,
            6: move,
            7: eat
        }

cdef class CellConfig:
    def __init__(self,
                 cell_size: int,
                 cell_mutation_chance: int,
                 cell_energy_to_live: int,
                 eat_gain_energy: int,
                 cells_available_actions_count: int,
                 CellActionsCostConfig actions_costs,
                 start_cell_energy: int,
                 max_cell_energy: int,
                 genome_size: int,
                 max_genome_value: int,
                 screen_config: ScreenConfig,
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
        self.max_genome_value = max_genome_value
        self.max_x_id = screen_config.window_width // cell_size
        self.max_y_id = screen_config.window_height // cell_size

cdef class GameConfig:
    def __init__(
            self,
            # Game settings
            seed: int,
            flip_interval: int = 120,
            # Screen settings
            tuple background_color = (180, 180, 180),
            int window_width = 1800,
            int window_height = 900,
            # Cell settings
            cell_size: int = 35,
            cell_mutation_chance: int = 100,
            cell_energy_to_live: int = 3,
            eat_gain_energy: int = 20,
            cells_available_actions_count: int = 5,
            start_cell_energy: int = 50,
            max_cell_energy: int = 150,
            genome_size: int = 64,
            max_genome_value: int = 64,
            # Cell actions const settings
            int check_energy = 1,
            int check_cell_in_front = 1,
            turn: int = 1,
            get_minerals_energy: int = 5,
            photosynthesis: int = 5,
            move: int = 26,
            eat: int = 2
    ):
        self.seed = seed
        actions_costs = CellActionsCostConfig(
            check_energy=check_energy,
            check_cell_in_front=check_cell_in_front,
            turn=turn,
            get_minerals_energy=get_minerals_energy,
            photosynthesis=photosynthesis,
            move=move,
            eat=eat
        )
        self.screen_config = ScreenConfig(background_color, window_width, window_height)
        self.cell_config = CellConfig(
            cell_size=cell_size,
            cell_mutation_chance=cell_mutation_chance,
            cell_energy_to_live=cell_energy_to_live,
            eat_gain_energy=eat_gain_energy,
            cells_available_actions_count=cells_available_actions_count,
            actions_costs=actions_costs,
            start_cell_energy=start_cell_energy,
            max_cell_energy=max_cell_energy,
            genome_size=genome_size,
            screen_config=self.screen_config,
            max_genome_value=max_genome_value
        )
        self.flip_interval = flip_interval
        self.stop = False
