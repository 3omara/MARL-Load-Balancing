#include "cell-individual-offset.h"


std::vector<double> CellIndividualOffset::OffsetList(40,0);

void CellIndividualOffset::setOffsetList(std::vector<double>& CioList)
{
		// OffstList = CioList; // Removed
		// Added
		for (unsigned int i = 0; i < CioList.size(); i++){
			OffsetList.at(i) += CioList.at(i);
		}
		//
}


std::vector<double> CellIndividualOffset::getOffsetList()
{
		return OffsetList;
}
