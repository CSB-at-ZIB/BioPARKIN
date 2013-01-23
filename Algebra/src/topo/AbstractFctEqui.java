package topo;

import util.Function;

public class AbstractFctEqui<E extends Element<E>,F extends Element<F>,G extends Function<E, F>, X extends AbstractTopo<E>>
		extends AbstractEqui<E,AbstractTopo<E>> {
	Function<E,F> fct;
	public AbstractFctEqui (Function<E,F> fct){
		super();
		if(fct!=null) this.fct = fct;
	}
	
	public AbstractTopo<E> equiClass(E element) {
		final E cp = element;
		final Function<E,F> fctCP = fct;
		return new AbstractTopo<E> (){
			public boolean contains(E element){
				fctCP.f(cp);
				F val1 = fctCP.getValue();
				fctCP.f(element);
				return val1.equals(fctCP.getValue());
			}
		};
	}
	
	public boolean isRelated(E first, E second) {
		if(fct==null) return false;
		fct.f(first);
		F val1 = fct.getValue();
		fct.f(second);
		return val1.equals(fct.getValue());
	}
	
}
