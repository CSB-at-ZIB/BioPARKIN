package topo;
import field.DoubleField;
public abstract class Metric<M extends ContiFct<M, PairedElement<E>, DoubleField, T, DoubleDim1<InRange>, AbstractEqui<PairedElement<E>,T>>, E extends Element<E>, T extends TopoSpace<T, PairedElement<E>>>
		implements ContiFct<M, PairedElement<E>, DoubleField, T, DoubleDim1<InRange>, AbstractEqui<PairedElement<E>,T>> {
	private PairedElement<E> arg;
	private DoubleField val;
	public Metric (){super();}
	
	public void f(PairedElement<E> arg) {
		if(arg!=null){ this.arg = arg; f();}
	}


	public PairedElement<E> getArgument() {return arg==null?null:arg;}

	
	public DoubleField getValue() {return val==null?null:val;}

	
	public DoubleDim1<InRange> coDomain() {return DoubleDim1.NON_NEGATIVE;}

	
	public T domain() {return arg==null?null:isInPreImage().equiClass(arg);}

	

	
	public AbstractEqui<PairedElement<E>, T> isInPreImage() {
		//TODO does it need to be implemented???
		final Metric<M,E,T> met = this;
		AbstractEqui<PairedElement<E>,T>preImag = new AbstractEqui<PairedElement<E>,T>(){

			@Override
			public T equiClass(PairedElement<E> element) {
				// TODO Auto-generated method stub
				return null;
			}

			public boolean isRelated(PairedElement<E> first, PairedElement<E> second) {
				met.f(first);
				DoubleField val1 = met.getValue();
				met.f(second);
				DoubleField val2 = met.val;
				return val1.equals(val2);
			}
			
		};
		return preImag;
	}

}
