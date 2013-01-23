package module;

import ring.Ring;

public interface LeftModule<M extends LeftModule<M, R>, R extends Ring<R>>
		extends Module<M, R> {
	public M multiply (R scalar);
}
