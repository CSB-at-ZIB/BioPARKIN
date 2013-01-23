package module;

import ring.Ring;

public interface RightModule<M extends RightModule<M, R>, R extends Ring<R>>
		extends Module<M, R> {
	public M multiply (R scalar);
}
