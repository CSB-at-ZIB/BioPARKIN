package module;

import field.AbstractField;

public interface VectorSpace<V extends VectorSpace<V, F>, F extends AbstractField<F>>
		extends CommModule<V, F> {
}
