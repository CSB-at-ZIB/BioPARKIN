package group;

import topo.Element;

public interface Monoid<M extends Monoid<M>> extends Element<M>{
	public M operate (M another);
}
