#include "cell-individual-offset.h"


std::vector<double> CellIndividualOffset::OffsetList(40,0);

void CellIndividualOffset::setOffsetList(std::vector<double>& CioList)
{
		// OffstList = CioList; // Removed
		// Added
		std::transform(OffsetList.begin(), OffsetList.end(), CioList.begin(),
               OffsetList.begin(), std::plus<double>());
		//
}


std::vector<double> CellIndividualOffset::getOffsetList()
{
		return OffsetList;
}
