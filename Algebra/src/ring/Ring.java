package ring;

import group.AbelGroup;

/**
 * Interface of algebraic rings
 * @author gmueller
 *
 * @param <R> the sub type
 */
public interface Ring<R extends Ring<R>> extends AbelGroup<R>{
	/**
	 * Returns the additive inverse of <code>this</code>,
	 * such that <code>addInverse().add(this).isZero()</code> returns true
	 * @return
	 */
	public R addInverse ();
	/**
	 * Returns true if this element commutes
	 * @return
	 */
	public boolean isCommutative ();
	/**
	 * Returns true, if <code>this</code> represents the zero element
	 * @return
	 */
	public boolean isZero();
	/**
	 * Returns the product <code>this * another</code>
	 * @param another
	 * @return
	 */
	public R multiply(R another);
}
