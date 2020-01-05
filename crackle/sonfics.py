#!/usr/bin/env python
'''Simple sonification functions.
'''

import copy
import music21 as m21
import numpy as np

########################################################################
########################################################################

def volume_vs_rhythm(
    xs,
    ys,
    x_min, x_max,
    y_min, y_max,
    stream = None,
    pitch = 'G#3',
    full_duration = 4.,
    velocity_scalar_min = 0., velocity_scalar_max = 1.,
):
    '''A function for sonifying data with rhythm as the x-axis and volume as
    the y axis.

    Args:
        velocity_scalar_min, velocity_scalar_max (floats):
    '''

    # Make copies so we can alter
    xs = copy.deepcopy( xs )
    ys = copy.deepcopy( ys )

    # Create a stream
    if stream is None:
        stream = m21.stream.Stream()

    # Conversion for units to axes
    x_to_dur = np.abs(
        full_duration / ( x_max - x_min )
    )
    y_to_vel = np.abs(
        ( velocity_scalar_max - velocity_scalar_min ) / ( y_max - y_min )
    )

    # Add on x-axis edges
    xs = np.insert( xs, 0, x_min )
    xs = np.insert( xs, -1, x_max )

    # Loop through notes
    notes = []
    for i, x in enumerate( xs ):

        # End of list
        if i == len( xs ) - 1:
            break

        # First note is a rest
        if i == 0:
            note = m21.note.Rest()
        else:
            note = m21.note.Note( pitch )

        # Alter note duration
        dx = xs[i+1] - x
        note.duration.quarterLength = dx * x_to_dur

        # Alter note volume
        if i != 0:
            note.volume.velocityScalar = ys[i-1] * y_to_vel

        notes.append( note )

    stream.append( notes )

    return stream
        
