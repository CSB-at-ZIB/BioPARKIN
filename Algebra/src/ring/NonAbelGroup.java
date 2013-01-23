package ring;

import group.Group;

/**
 * The interface for the implementation of non-abelian groups
 * @author gmueller
 *
 * @param <N>
 */
public interface NonAbelGroup<N extends NonAbelGroup<N>> extends Group<N> {
	/**
	 * Returns the product <tt>this * another</tt>
	 * @param another another non abelian object
	 * @return the product
	 */
	public N multiply (N another);
}
