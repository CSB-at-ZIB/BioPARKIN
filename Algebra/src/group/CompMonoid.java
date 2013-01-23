package group;
/**
 * Combines the {@link Monoid} interface an the {@link Comparable}
 * interface
 * @author bzfmuell
 *
 * @param <C> the type of the implementing class
 */
public interface CompMonoid<C extends CompMonoid<C>> extends Monoid<C> , Comparable<C>{}
