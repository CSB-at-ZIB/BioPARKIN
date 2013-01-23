package module;

import java.util.Set;

import ring.Ring;
/**
 * The finitely generated {@link R}-module interface:
 * @author adin
 *
 * @param <M>
 * @param <R>
 */
public interface FiniteGenMod<M extends FiniteGenMod<M, R>, R extends Ring<R>>
		extends Module<M, R> {
	public Set<FiniteGenMod<M,R>> getGenerators();
}
