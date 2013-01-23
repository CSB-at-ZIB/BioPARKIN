package topo;


public abstract class AbstractContiFct<A extends AbstractContiFct<A, E, F, X, Y,R>, E extends Element<E>, F extends Element<F>, X extends AbstractTopo<E>, Y extends TopoSpace<Y, F>, R extends EquiRel<E,AbstractTopo<E>,R>>
	implements ContiFct<A, E, F, AbstractTopo<E>, Y, R>{
	private E arg;
	private F val;
	private AbstractTopo<E> dom;
	private Y cod;
	
	public AbstractContiFct(){}
	
	public void f(E arg) {
		if(dom.contains(arg)){this.arg = arg;f();}
	}

	
	public E getArgument() {return arg==null?null:arg;}

	
	public F getValue() {
		if(arg==null) return null;
		f();
		return val==null?null:val;
	}

	
	public Y coDomain() {return cod;}

	
	public AbstractTopo<E> domain() {return dom;}

	
	public A extend(
			AbstractTopo<E> superSet) {
		// TODO Auto-generated method stub
		return null;
	}

	
	public R isInPreImage() {
		// TODO Auto-generated method stub
		return null;
	}

	
	public AbstractContiFct<A,E,F,X,Y,R> restrict(
			AbstractTopo<E> subset) {
		final AbstractContiFct<A,E,F,X,Y,R> cp = this;
		AbstractContiFct<A,E,F,X,Y,R> res = new AbstractContiFct<A,E,F,X,Y,R>(){
			public void f(){
				if(arg==null) return;
				if(dom.contains(arg)){
					cp.f(arg);
					val = cp.val;
				}
			}
		};
		res.dom = subset;
		return res;
		
	}
	
}