package group;
/**
 * The abstract Abelian group class 
 * @author muellerg
 *
 * @param <A>
 */
public abstract class AbstractAbel<A extends AbelGroup<A>> implements
		AbelGroup<A> {
	/**
	 * Constructs an empty instance
	 */
	public AbstractAbel (){}
	/**
	 * The operation is defined via the
	 * {@link AbelGroup#add(A)} method
	 */
	public A operate(A another) {return add(another);}

}
