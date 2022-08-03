#include <inery/inery.hpp>
#include <string>

using namespace inery;
using namespace std;

class [[inery::contract("sto")]] sto : public contract {
    public:
        using contract::contract;
        sto(name reciever, name code, datastream<const char*> ds ) : contract(reciever, code, ds) {}

	struct [[inery::table("tabla")]] tabla {
		uint64_t	id;
		string	predmet;
		uint64_t primary_key() const {return id; }
	};
	typedef inery::multi_index<"tabla"_n, tabla> table_inst0;


	[[inery::action]] void crtabla (string predmet) {
		table_inst0  tabla(get_self(), get_self().value);
		tabla.emplace(get_self(), [&](auto &row){
			row.id = tabla.available_primary_key();
			row.predmet = predmet;
		});
	}
	[[inery::action]] void uptabla (uint64_t id, string predmet) {
		table_inst0  tabla(get_self(), get_self().value);
		auto itr = tabla.find(id);
		check(itr != tabla.end(), "No entity with that id ");
		tabla.modify(itr, get_self(), [&](auto &row){
			row.predmet = predmet;
		});
	}
	[[inery::action]] void dltabla (uint64_t id) {
		table_inst0  tabla(get_self(), get_self().value);
		auto itr = tabla.find(id);
		check(itr != tabla.end(), "No entity with that id ");
		tabla.erase(itr);
	}
};