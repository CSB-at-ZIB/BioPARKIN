package homomorphism;

import ring.Ring;
import module.Module;

public interface ModuleHomo<H extends ModuleHomo<H, M, N, R, S>, M extends Module<M, R>, N extends Module<N, S>, R extends Ring<R>, S extends Ring<S>>
		extends Module<H, R>, GroupHomo<H,M,N> {

}
