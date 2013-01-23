package module;

import ring.Ring;
/**
 * The multi linear form interface: let <tt>M</tt> be a <tt>R</tt> module,
 * an <tt>n</tt>-form is a mapping <br /><tt>f : M^n -> R</tt>, <tt>(x_1,...,x_n) |-> sum_(k in N^n) a_k x_k_1^t_k_1...x_k_n^t_k_n</tt>
 * <br />Note, that this map is linear in each component
 * @author adin
 *
 * @param <M>
 * @param <N>
 * @param <R>
 */
public interface MultiForm<M extends MultiForm<M, R, N>, R extends Ring<R>,N extends Module<N,R>>
		extends Module<M, R> {
	/**
	 * Evaluates this multi linear form and returns the scalar
	 * value
	 * @param arg the argument
	 * @return the scalar value
	 */
	public R eval (N[] arg);
}
