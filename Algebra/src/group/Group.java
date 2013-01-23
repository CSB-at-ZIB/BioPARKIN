package group;

import ring.NonAbelGroup;

/**
 * Dummy interface for the group implementation: two sub interfaces intended
 * <ol><li>{@link AbelGroup} an abelian group (implementing add)</li>
 * <li>{@link NonAbelGroup} a non-abelian group (implementing multiply)</li></ol>
 * @author gmueller
 *
 */
public interface Group<G extends Group<G>> extends Monoid<G>{}
