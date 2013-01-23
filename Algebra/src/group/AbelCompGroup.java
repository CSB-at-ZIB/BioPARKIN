package group;

public interface AbelCompGroup<A extends AbelCompGroup<A>> extends AbelGroup<A>, CompMonoid<A>{}
