package homomorphism;

import field.AbstractField;
import module.VectorSpace;
import module.CommModule;
/**
 * The vector space (VS) homomorphism interface over some algebraic field of type <code>F</code>
 * @author bzfmuell
 *
 * @param <H> the VS homomorphism type
 * @param <V> the preimage VS type
 * @param <W> the image VS type
 * @param <F> the field type
 */
public interface VectorSHomo<H extends VectorSHomo<H,V,W,F>, V extends VectorSpace<V, F>, W extends VectorSpace<W, F>, F extends AbstractField<F>>
		extends ModuleHomo<H, V, W, F, F>, CommModule<H,F> {
	
}
