package topo;
/**
 * The element interface: the only method to implement is {@link Element#equals(Element)}
 * @author bzfmuell
 *
 * @param <E> the subtype of <code>Element</code>
 */
public interface Element<E extends Element<E>> {
	/**
	 * The only method to implement: returns true iff
	 * <tt>this == another</tt>
	 * @param another another element
	 * @return true if both are equal
	 */
	public boolean equals(E another);
}
