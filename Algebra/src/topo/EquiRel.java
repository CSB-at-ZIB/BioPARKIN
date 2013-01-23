package topo;
/**
 * The equivalence relation interface: any equivalence relation must
 * be
 * <ol>
 * <li><b>reflexive</b>: <tt>x.isRelated(x)</tt> must return true for any element <tt>x</tt> in some equivalence class</li>
 * <li><b>symmetric</b>: <tt>x.isRelated(y)&&y.isRelated(x)</tt> must return true for any two elements <tt>x, y</tt> in the same equivalence class</li>
 * <li><b>transitive</b>: if <tt>x.isRelated(y)</tt> and <tt>y.isRelated(z)</tt> return true so must <tt>x.isRelated(z)</tt></li>
 * </ol>
 * @author bzfmuell
 *
 * @param <E> the element type
 * @param <S> the set type
 */
public interface EquiRel<E extends Element<E>, S extends Set<E,S>, R extends EquiRel<E,S,R>> extends Relation<E,R> {
	/**
	 * Returns the equivalence class specified by the argument
	 * <tt>element</tt>
	 * @param element the element
	 * @return the equivalence class
	 */
	public S equiClass(E element);
}
