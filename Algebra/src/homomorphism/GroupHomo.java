package homomorphism;

import group.Group;

public interface GroupHomo<X extends GroupHomo<X,G,H>, G extends Group<G>, H extends Group<H>> extends
		MonoidHomo<X,G,H> {

}
