package topo;

import util.Function;
/**
 * The continuous function interface between topological spaces
 * @author bzfmuell
 *
 * @param <C> the type of the function
 * @param <E> the preimage's type
 * @param <F> the image's type
 * @param <X> the preimage set's type
 * @param <Y> the image set's type
 */
public interface ContiFct<C extends ContiFct<C,E, F, X, Y,R>, E extends Element<E>, F extends Element<F>, X extends TopoSpace<X,E>, Y extends TopoSpace<Y,F>, R extends EquiRel<E,X,R>>
		extends Function<E, F> {
	public Y coDomain();
	public X domain();
	/**
	 * Returns the extension of this function
	 * on a super set. <b>Note</b>, the following expression
	 * must return true: <tt>superSet.isSuperSet(this.domain())</tt> 
	 * @param superSet the super set
	 * @return the extension
	 */
	public ContiFct<C,E,F,X,Y,R> extend (X superSet);
	/**
	 * Returns the equivalence relation, such that 
	 * <tt>isInPreImage().isRelated(this.getValue())
	 * @return
	 */
	public R isInPreImage();
	public ContiFct<C,E,F,X,Y,R> restrict(X subset);
	
}
