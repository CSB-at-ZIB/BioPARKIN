package group;

import util.InMap;

public interface Action<A extends Action<A, G, X>, G extends Group<G>, X>
		extends InMap<X> {
	public X act(G g, X arg);
}
