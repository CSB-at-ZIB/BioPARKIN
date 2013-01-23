package topo;
/**
 * The abstract topological space class: the only method to implement:
 * {@link AbstractTopo#contains(E)}
 * @author bzfmuell
 *
 * @param <E> the element type
 */
public abstract class AbstractTopo<E extends Element<E>> implements
		TopoSpace<AbstractTopo<E>, E> {

	private boolean isEmpty, isFull;
	private boolean  isOpen, isClosed;
	/**
	 * Default constructor
	 */
	public AbstractTopo (){}
	
	public AbstractTopo<E> complement() {
		final AbstractTopo<E> cp = this;
		AbstractTopo<E> compl = new AbstractTopo<E> (){
			
			public boolean contains (E element){
				return !cp.contains(element);
			}

			
		};
		if(isFull) compl.isEmpty = true;
		if(!isOpen&&isClosed){compl.isOpen  = true;isClosed = false;}
		return compl;
	}
	
	public boolean equals(Object o){
		if(this==o) return true;
		if(!(o instanceof AbstractTopo)) return false;
		@SuppressWarnings("unchecked")
		AbstractTopo<E> cp = (AbstractTopo<E>) o;
		return intersect(cp.complement()).isEmpty()&&complement().intersect(cp).isEmpty();
	}
	
	public AbstractTopo<E> intersect(AbstractTopo<E> another) {
		final AbstractTopo<E> cp1 = this, cp2 = another;
		if(isEmpty||another.isEmpty) return emptySet();
		return new AbstractTopo<E> (){
			public boolean contains(E element){
				return cp1.contains(element)&&cp2.contains(element);
			}

		};
	}

	public boolean isEmpty(){return isEmpty;}
	
	public boolean isOpen (){return isOpen;}
	
	public AbstractTopo<E> union(AbstractTopo<E> another) {
		final AbstractTopo<E> cp1 = this, cp2 = another;
		return new AbstractTopo<E> (){
			public boolean contains(E element){return cp1.contains(element)||cp2.contains(element);}

			
			
		};
	}

	
	

	
	public boolean isSuperSet(AbstractTopo<E> another) {
		if(this==null) return false;
		if(another==null) return true;
		return intersect(another).equals(another);
	}

	
	public boolean isSubSet(AbstractTopo<E> another) {
		if(this==null) return true;
		if(another==null) return false;
		return intersect(another).equals(this);
	}
	
	public void setIsEmpty(boolean isEmpty){this.isEmpty = isEmpty;isFull = !isEmpty;}
	
	public void setIsOpen (boolean isOpen){this.isOpen = isOpen;isClosed = !isOpen;}
	/**
	 * Returns the empty set of type <tt>&ltE&gt</tt>. The method {@link AbstractTopo#contains(E)}
	 * returns false for any (even null) element
	 * @return the empty set
	 */
	public static <E extends Element<E>> AbstractTopo<E> emptySet(){
		AbstractTopo<E> empty = new AbstractTopo<E> (){public boolean contains(E element){return false;}};
		empty.isEmpty = true;
		return empty;
	}
	/**
	 * Returns the complement set of the empty set of type <tt>&ltE&gt</tt>.
	 * The method {@link AbstractTopo#contains(E)} will return true for any
	 * non-null element
	 * @return the full set
	 */
	public static <E extends Element<E>> AbstractTopo<E> fullSet (){
		return new AbstractTopo<E> (){public boolean contains(E element){return element!=null?true:false;}};
	}

}
