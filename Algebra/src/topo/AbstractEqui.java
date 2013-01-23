package topo;

public abstract class AbstractEqui<E extends Element<E>,S extends Set<E,S>> extends
		AbstractRelation<E, AbstractEqui<E,S>> implements EquiRel<E,S,AbstractEqui<E,S>>{
	public AbstractEqui (){super();}

	
	public boolean isEmpty() {return false;}

	
	public boolean isOpen() {return false;}

	
	public boolean isClosed() {return true;}

	
}
