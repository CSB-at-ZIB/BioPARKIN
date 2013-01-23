package manifold;

import topo.Element;
import topo.TopoSpace;

public interface ChartArea<C extends ChartArea<C, E>, E extends Element<E>>
		extends TopoSpace<C, E> {

}
