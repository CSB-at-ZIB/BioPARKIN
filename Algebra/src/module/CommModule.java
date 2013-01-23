package module;

import ring.AbstractCommRing;
/**
 * Interface for all modules over some commutative ring of type <tt>R</tt>
 * @author bzfmuell
 *
 * @param <C> the (implementing) module type
 * @param <R> the the ring type
 */
public interface CommModule<C extends CommModule<C, R>, R extends AbstractCommRing<R>>
		extends RightModule<C, R>, LeftModule<C,R> {
}
