package field;

import ring.Ring;

/**
 * The field interface: note that any implementing class, the method
 * {@link Ring#isCommutative()} must return true
 * @author adin
 *
 * @param <F>
 */
public interface Field<F extends Field<F>> extends Ring<F> {
	/**
	 * Returns true if <tt>this.isZero()</tt> returns false
	 * @return
	 */
	public boolean isUnit ();
	/**
	 * Returns the multiplicative inverse
	 * @return
	 */
	public F inverse ();
}
