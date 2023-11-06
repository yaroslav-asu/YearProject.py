cdef class ScreenConfig:
    cdef public tuple background_color
    cdef public tuple border_color
    cdef public int window_width
    cdef public int window_height

cdef class CellActionsCostConfig:
    cdef public dict actions_costs

cdef class CellConfig:
    cdef public int cell_size
    cdef public int cell_mutation_chance
    cdef public int cell_energy_to_live
    cdef public int eat_gain_energy
    cdef public int cells_available_actions_count
    cdef public dict actions_costs
    cdef public int start_cell_energy
    cdef public int max_cell_energy
    cdef public int genome_size
    cdef public int max_x_id
    cdef public int max_y_id

cdef class GameConfig:
    cdef public int seed
    cdef public CellConfig cell_config
    cdef public ScreenConfig screen_config
    cdef public int flip_interval
    cdef public bint stop
