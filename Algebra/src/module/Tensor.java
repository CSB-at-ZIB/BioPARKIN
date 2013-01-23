package module;

import ring.Ring;
/**
 * The general tensor product interface of two modules over some ring of type <code>R</code>
 * @author bzfmuell
 *
 * @param <T> the tensor product type
 * @param <M> the <code>R</code>-(right) module type 
 * @param <N> the <code>R</code>-(left) module type
 * @param <R> the ring type
 */
public interface Tensor<T extends Tensor<T, M, N, R>, M extends RightModule<M, R>, N extends LeftModule<N, R>, R extends Ring<R>>
		extends Module<T, R> {
	/**
	 * Returns the tensor product of the (right) module element <tt>left</tt> and
	 * the (left) module element <tt>right</tt>:<br />
	 * <tt>left &#8855 right</tt>, where <tt>&#8855</tt> stands for 'tensorized'
	 * @param left the 'left' factor
	 * @param right the 'right' factor
	 * @return the tensor product <tt>left &#8855 right</tt>
	 */
	public T tensorize (M left, N right);
}
