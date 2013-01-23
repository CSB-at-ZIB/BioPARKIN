package group;

import ring.NonAbelGroup;

/**
 * The abstract non-Abelian group class
 * @author muellerg
 *
 * @param <N>
 */
public abstract class AbstractNAG<N extends AbstractNAG<N>> implements
		NonAbelGroup<N> {
	/**
	 * Constructs an empty instance
	 */
	public AbstractNAG (){}
	/**
	 * The operation is defined via the
	 * {@link NonAbelGroup#multiply(N)} method
	 */
	public N operate(N another) {return multiply(another);}

}
