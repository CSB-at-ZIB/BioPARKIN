package group;
/**
 * The interface for the implementation of abelian groups
 * @author gmueller
 *
 * @param <A>
 */
public interface AbelGroup<A extends AbelGroup<A>> extends Group<A> {
	/**
	 * The standard operation on each abelian group
	 * @param another
	 * @return
	 */
	public A add(A another);
}
