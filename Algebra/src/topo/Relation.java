package topo;
/**
 * The relation interface: defines relations on some set.
 * @author bzfmuell
 *
 * @param <E> the element type
 */
public interface Relation<E extends Element<E>, R extends Relation<E,R>> {
	/**
	 * Returns the base point of this relation:
	 * that is some elements <tt>x,y</tt> such that
	 * <tt>this.isRelated(x,y)</tt> returns true
	 * @return the base point
	 */
	public PairedElement<E> basePoint();
	/**
	 * Returns the inverse relation: that is
	 * if <tt>this.isRelated(x,y)</tt> returns false for 
	 * some elements <tt>x,y</tt> then <tt>inverse().isRelated(x,y)</tt> returns true
	 * @return the inverse relation
	 */
	public R  inverse();
	/**
	 * Returns true if this relation is closed (in the topological sense)
	 * @return true if this relation is closed
	 */
	public boolean isClosed();
	/**
	 * Returns true if <tt>first</tt> and <tt>second</tt> are related
	 * @param first the first element
	 * @param second the second element
	 * @return true if both elements are related
	 */
	public boolean isRelated(E first, E second);
}
