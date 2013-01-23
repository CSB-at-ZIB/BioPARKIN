package topo;
/**
 * The basic (mathematical) set interface: there are five methods to implement:
 * <ol>
 * <li>{@link Set#contains(E)}: returns true if some element is contains in this set</li>
 * <li>{@link Set#intersect(S)}: returns the intersection of this and another set of the same type</li>
 * <li>{@link Set#isEmpty()}: returns true if this is the empty set</li>
 * <li>{@link Set#isOpen()}: returns true if this set is open</li>
 * <li>{@link Set#union(S)}: returns the union set of this and some other set of the same type</li>
 * </ol>
 * @author bzfmuell
 *
 * @param <E> the subtype of the element
 * @param <S> the subtype of the set
 */
public interface Set<E extends Element<E>,S extends Set<E,S>> {
	/**
	 * Returns true if this set contains the <tt>element</tt>
	 * @param element the element to test
	 * @return true if this set contains the element
	 */
	public boolean contains(E element);
	/**
	 * Returns the intersection of <tt>this</tt> and
	 * <tt>another</tt> set
	 * @param another some other set
	 * @return the intersection
	 */
	public S intersect(S another);
	/**
	 * Returns true if this set is empty (no elements)
	 * @return true if empty
	 */
	public boolean isEmpty();
	/**
	 * Returns true if this set is open
	 * @return true if open
	 */
	public boolean isOpen();
	/**
	 * Returns the union of <tt>this</tt> and <tt>another</tt>
	 * set instance
	 * @param another some other set
	 * @return the union
	 */
	public S union(S another);
}

