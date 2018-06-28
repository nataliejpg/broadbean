# This file contains the Element definition

from typing import Union, Dict, List
from copy import deepcopy, copy

import numpy as np

from broadbean.segment import Segment, ContextDict

ChannelIDType = Union[int,str]

class ElementDurationError(Exception):
    pass


class Element:
    """
    Object representing an element. An element is a collection of waves that
    are to be run simultaneously. The element consists of a number of channels
    that are then each filled with anything of the appropriate length.
    """
    def __init__(self, segments:Dict[ChannelIDType, Segment]={},
                 sequencing:Dict[str, int]={},
                 local_context={}):
        self.segments = segments
        self.sequencing = sequencing
        self.local_context = local_context
        # make sequencing options kwargs
        # define jump target maybe as element reference that gets dereferenced in sequence?
        # self._sequencing[pos] = {'twait': wait, 'nrep': nreps,
        #                          'jump_target': jump, 'goto': goto,
        #                          'jump_input': 0}

    def get_duration(self, **context):
        """
        Returns the duration in seconds of the element, if said duration is
        well-defined. Else raises an error.
        """
        durations = set(s.get('duration', **context) for _, s in self.segments.items())
        if len(durations) != 1:
            raise ElementDurationError
        return durations.pop()

    # def apply_context(self, **context: ContextDict) -> None:
    #     for channel, segment in self.segments.items():
    #         segment.apply_context(**context)

    def __copy__(self):
        return Element(deepcopy(self.segments),
                       deepcopy(self.sequencing))

    # I think this should go into the main forge function. There is no point of forging an element outside of a sequence. This is different for a Segment.
    def forge(self, SR, context, include_time=False):
        context_arg = copy(context)
        context_arg.update(self.local_context)
        return {channel_id: segment.forge(SR, **context_arg) for channel_id, segment in self.segments.items()}


    # TODO: add methods/operators for stacking, concatenation, equality
