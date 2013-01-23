package ring;

import group.CompMonoid;

public interface NonAbelGrp<N extends NonAbelGrp<N>> extends NonAbelGroup<N>,
		CompMonoid<N> {

}
