package topo;
/**
 * The topological space interface: sub interface of {@link Set}
 * @author bzfmuell
 *
 * @param <T> the type of the topo space
 * @param <E> the type of the element
 */
public interface TopoSpace<T extends TopoSpace<T,E>, E extends Element<E>>
		extends Set<E, T> {
	/**
	 * Returns the complementary topo space of this
	 * @return the complement
	 */
	public T complement();
	/**
	 * Returns true if this is the super set
	 * of <tt>another</tt>
	 * @param another some other topo space
	 * @return
	 */
	public boolean isSuperSet(T another);
	/**
	 * Returns true if this is a sub set of
	 * <tt>another</tt>
	 * @param another
	 * @return
	 */
	public boolean isSubSet (T another);
}
