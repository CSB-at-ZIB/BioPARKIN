package module;

import ring.Ring;
import util.Tupleable;
import group.AbelGroup;
/**
 * The module interface over some ring of type {@link R}
 * @author adin
 *
 * @param <M> the type of the implementing submodule
 * @param <R> the type of the ring
 */
public interface Module<M extends Module<M,R>, R extends Ring<R>> extends AbelGroup<M>, Tupleable<R> {
	public M ringAct (R scalar);
	public boolean isZero();
}
